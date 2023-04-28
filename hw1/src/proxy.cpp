#include "proxy.h"
#include <algorithm>

GetResultController::GetResultController(const std::unordered_map<std::string, std::shared_ptr<Serializer>>* serializers)
: Serializers(serializers) {}

void GetResultController::Handle(Request &request, StreamResponse &response) {
    std::string method = htmlEntities(request.get("method", ""));
    if (method.empty()) {
        response << "Please, provide name of serialization method" << endl;
        return;
    }
    std::shared_ptr<Serializer> serializer;
    try {
        std::transform(method.begin(), method.end(), method.begin(), [](unsigned char c){ return std::tolower(c); });
        serializer = Serializers->at(method);
    } catch (...) {
        response << "No such serialization method available" << endl;
        return;
    }
    response << Tester.Test(serializer, method) << endl;
}

void GetResultController::setup() {
    addRoute("GET", "/get_result", GetResultController, Handle);
}


ProxyServer::ProxyServer(int port,  GetResultController&& controller)
 : Server(port), Controller(controller) {
    Server.registerController(&Controller);
}

void ProxyServer::Start() {
    Server.start();
    while (true) {
        sleep(10);
    }
}