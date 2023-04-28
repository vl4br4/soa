#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <unordered_map>
#include <memory>
#include <mongoose/Server.h>
#include <mongoose/WebController.h>
#include "serializers/Serializer.h"
#include "SerializationTester.h"


using namespace Mongoose;
using namespace std;

class GetResultController : public WebController {
public: 
    GetResultController(const std::unordered_map<std::string, std::shared_ptr<Serializer>>* serializers);
    void Handle(Request &request, StreamResponse &response);
    void setup();
private:
    const std::unordered_map<std::string, std::shared_ptr<Serializer>>* Serializers;
    SerializationTester Tester;
};

class ProxyServer {
public:
    ProxyServer(int port, GetResultController&& controller);
    void Start();
private:
    Server Server;
    GetResultController Controller;
};