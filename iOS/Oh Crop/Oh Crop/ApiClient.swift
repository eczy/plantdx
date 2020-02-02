//
//  ApiClient.swift
//  Oh Crop
//
//  Created by Evan Czyzycki on 2/2/20.
//  Copyright © 2020 Evan Czyzycki. All rights reserved.
//

import Foundation

class ApiClient {
    static var shared = ApiClient()
    init() {}
    func post(url: URL, body: Data, completionHandler: @escaping (Data?, URLResponse?, Error?) -> Void = {_,_,_ in }) {
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.httpBody = body
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")  // the request is JSON
        let task = URLSession.shared.dataTask(with: request, completionHandler: completionHandler)
        task.resume()
    }
}
