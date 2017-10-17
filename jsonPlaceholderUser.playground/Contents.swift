//: Playground - noun: a place where people can play

import UIKit
import PlaygroundSupport

enum BackendError: Error {
    case urlError(reason: String)
    case objectSerialization(reason: String)
}

struct Address: Codable {
    var city: String
    var street: String
    var zipcode: String
}
struct User: Codable {
    var id: Int
    var name: String
    var email: String
    var phone: String
    var address: Address
    
    static func endpointForID(_ id: Int) -> String {
        return "https://jsonplaceholder.typicode.com/users/\(id)"
    }
    
    static func userByID(_ id: Int, completionHandler: @escaping (User?, Error?) -> Void) {
        let urlEndpoint = User.endpointForID(1)
        
        guard let url = URL(string: urlEndpoint) else {
            print("Error: Can't create URL")
            let error = BackendError.urlError(reason: "Could not create URL")
            completionHandler(nil, error)
            return
        }
        
        let request = URLRequest(url: url)
        let session = URLSession.shared
        
        let task = session.dataTask(with: request) { data, response, error in
            guard let responseData = data else {
                print("Error: did not recieve data")
                completionHandler(nil, error)
                return
            }
            guard error == nil else {
                completionHandler(nil, error)
                return
            }
            
            let decoder = JSONDecoder()
            do {
                let user = try decoder.decode(User.self, from: responseData)
                completionHandler(user, nil)
            } catch let error{
                print("Error: Data to JSON conversion failed")
                print(error)
                completionHandler(nil, error)
            }
        }
        task.resume()
    }
}

func getUser(_ idNumber: Int) {
    User.userByID(idNumber) { user, error in
        if let error = error {
            // got an error in getting the data, need to handle it
            print("error calling get on USERs")
            print(error)
            return
        }
        
        guard let user = user else {
            print("error getting user: result is nil")
            return
        }
        
        debugPrint("debug: ", user)
        print("reg: ", user)
        //print(user.address)
    }
    
}


getUser(1)


PlaygroundPage.current.needsIndefiniteExecution = true

