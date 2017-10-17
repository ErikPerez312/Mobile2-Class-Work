//: Playground - noun: a place where people can play

import UIKit
import PlaygroundSupport

enum Result<T> {
    case success(T)
    case failure(NetworkError)
}

enum NetworkError: Error {
    case couldNotParse
    case noData
    case networkError
}

struct AirBNBListing {
    var bathrooms: Double
    var bedrooms: Int
    var starRating: Double
    
    init(bathrooms: Double, bedrooms: Int, starRating: Double) {
        self.bathrooms = bathrooms
        self.bedrooms = bedrooms
        self.starRating = starRating
    }
}
struct ListingList: Decodable {
    let search_results: [AirBNBListing]
}

extension AirBNBListing: Decodable {
    enum Keys: String, CodingKey {
        case listing
    }
    
    enum ListingKeys: String, CodingKey {
        case bathrooms
        case bedrooms
        case starRating = "star_rating"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: Keys.self)
        let listingContainer = try container.nestedContainer(keyedBy: ListingKeys.self, forKey: .listing)
        
        let bathrooms = try listingContainer.decode(Double.self, forKey: .bathrooms)
        let bedrooms = try listingContainer.decode(Int.self, forKey: .bedrooms)
        let starRating = try listingContainer.decode(Double.self, forKey: .starRating)
        
        self.init(bathrooms: bathrooms, bedrooms: bedrooms, starRating: starRating)
    }
}

class Networking {
    func getListing(completionHandler: @escaping (Result<[AirBNBListing]>) -> Void) {
        let baseURL = URL(string:"https://api.airbnb.com/v2//search_results?key=915pw2pnf4h1aiguhph5gc5b2")!
        let session = URLSession.shared
        let request = URLRequest(url: baseURL)
        
        session.dataTask(with: request) { data, response, error in
            if let data = data {
                guard let list = try? JSONDecoder().decode(ListingList.self, from: data) else {
                    return completionHandler(Result.failure(.couldNotParse))
                }
                
                let listings = list.search_results
                completionHandler(Result.success(listings))
            }
        }.resume()
    }
}

let netResults = Networking()
let listingss = netResults.getListing { listing in
    print(listing)
}





PlaygroundPage.current.needsIndefiniteExecution = true
