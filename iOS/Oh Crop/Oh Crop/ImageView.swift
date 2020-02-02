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
        let sortedResults = zippedResults.sorted { $0.1.floatValue > $1.1.floatValue }.prefix(3)
        var text = ""
        for result in sortedResults {
            let prob = String(format: "%.2f", result.1.floatValue)
            text += "\u{2022} \(labels[result.0]) - \(prob) \n\n"
        }
        self.text = text
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
                Spacer()
                Button(action: {
                    self.useCamera = true
                    self.showImagePicker = true
                }) {
                    Text("Take picture")
                }
                .disabled(!UIImagePickerController.isSourceTypeAvailable(.camera))
                Spacer()
            }
            .padding(.top, 10)
            Button(action: self.classifyImage) {
                Text("Classify")
            }.padding(.top, 20)
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
