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
    @State var UserImage = Image("user")
    
    private lazy var module: TorchModule = {
        if let filePath = Bundle.main.path(forResource: "model", ofType: "pt"),
            let module = TorchModule(fileAtPath: filePath) {
            return module
        } else {
            fatalError("Can't find the model file!")
        }
    }()
    
    private lazy var labels: [String] = {
        if let filePath = Bundle.main.path(forResource: "words", ofType: "txt"),
            let labels = try? String(contentsOfFile: filePath) {
            return labels.components(separatedBy: .newlines)
        } else {
            fatalError("Can't find the text file!")
        }
    }()
    
    var body: some View {
        VStack {
            UserImage
                .resizable()
                .frame(width: 200, height: 200)
                .scaledToFit()
                .background(Color.gray)
//                .cornerRadius(200)
                .clipped()
            Button(action: {self.showImagePicker = true}) {
                Text("Choose from camera roll")
            }
            .padding(.top, 10)
        }
        .sheet(isPresented: $showImagePicker) {
            ImagePicker(showImagePicker: self.$showImagePicker, pickedImage: self.$UserImage)
        }
        
    }
}
    
    struct ImageView_Previews: PreviewProvider {
        static var previews: some View {
            ImageView()
        }
}
