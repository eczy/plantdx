//
//  ImageView.swift
//  Oh Crop
//
//  Created by Evan Czyzycki on 2/1/20.
//  Copyright © 2020 Evan Czyzycki. All rights reserved.
//

import SwiftUI

struct ImageView: View {
    
    @State var showCameraView = false
    @State var showImagePicker = false
    @State var UserImage: UIImage = UIImage() {
        didSet {
            print("Image changed!")
        }
    }
    @State var text: String = ""
    @State var useCamera = false
    
    private var module: TorchModule = {
        if let filePath = Bundle.main.path(forResource: "model", ofType: "pt"),
            let module = TorchModule(fileAtPath: filePath) {
            return module
        } else {
            fatalError("Can't find the model file!")
        }
    }()
    
    private var labels: [String] = {
        if let filePath = Bundle.main.path(forResource: "labels", ofType: "txt"),
            let labels = try? String(contentsOfFile: filePath) {
            return labels.components(separatedBy: .newlines)
        } else {
            fatalError("Can't find the text file!")
        }
    }()
    
    func classifyImage(){
        let resizedImage = $UserImage.wrappedValue.resized(to: CGSize(width: 224, height: 224))
        guard var pixelBuffer = resizedImage.normalized() else {
            return
        }
        guard let outputs = module.predict(image: UnsafeMutableRawPointer(&pixelBuffer)) else {
            return
        }
        let zippedResults = zip(labels.indices, outputs)
        let sortedResults = zippedResults.sorted { $0.1.floatValue > $1.1.floatValue }.prefix(1)
        var text = ""
        for result in sortedResults {
            let prob = String(format: "%.2f", result.1.floatValue * 100)
            text += "\(labels[result.0]) - \(prob)% \n\n"
        }
        self.text = text
        
        var disease_name = labels[sortedResults[0].0].split(separator: ":")[1]
        disease_name.removeFirst()
        let json: [String: Any] = [
            "disease_name": disease_name
//            "locale": String(Locale.current.languageCode!),
//            "timestamp": Date().timeIntervalSinceReferenceDate
        ]
        let jsonData = try! JSONSerialization.data(withJSONObject: json) as Data
        if let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString)
        }
        ApiClient.shared.post(url: URL(string: "https://us-central1-hacksc2020-267002.cloudfunctions.net/gcf_hacksc/hacksc_http")!, body: jsonData) {
            data, response, error in
            
            if error != nil || data == nil {
                print("Client error!")
                return
            }
            
            guard let response = response as? HTTPURLResponse, (200...299).contains(response.statusCode) else {
                print("Server error!")
                return
            }
            
//            guard let mime = response.mimeType, mime == "application/json" else {
//                print("Wrong MIME type!")
//                return
//            }
            
            do {
                let json = try JSONSerialization.jsonObject(with: data!, options: []) as! [String: Any]
                if let treatments = json["treatments"] as? [String] {
                    self.text += "\nTreatment: \n" + treatments[0]
                }
            } catch {
                print("JSON error: \(error.localizedDescription)")
            }
            
        }
    }
    
    var body: some View {
        VStack {
            Image(uiImage: UserImage)
                .resizable()
                .scaledToFit()
                .background(Color.gray)
                .clipped()
                .padding(20)
            HStack {
                Spacer()
                Button(action: {
                    self.useCamera = false
                    self.showImagePicker = true
                }) {
                    Text("Choose picture")
                }
                .padding()
                Spacer()
                Button(action: {
                    self.useCamera = true
                    self.showImagePicker = true
                }) {
                    Text("Take picture")
                }
                .padding()
                .disabled(!UIImagePickerController.isSourceTypeAvailable(.camera))
                Spacer()
            }
            .padding(10)
            Button(action: self.classifyImage) {
                Text("Classify")
            }
            .padding(20)
            
            Text(self.text)
        }
        .sheet(isPresented: $showImagePicker) {
            ImagePicker(showImagePicker: self.$showImagePicker, pickedImage: self.$UserImage, useCamera: self.$useCamera)
        }
    }
}

struct ImageView_Previews: PreviewProvider {
    static var previews: some View {
        ImageView()
    }
}
