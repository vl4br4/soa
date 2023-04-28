#include <string>
#include "proxy.h"
#include "serializers/NativeSerializer.h"
#include "serializers/XMLSerializer.h"
#include "serializers/JSONSerializer.h"
#include "serializers/ProtoSerializer.h"
#include "SerializationTester.h"
#include <nlohmann/json.hpp>

const static std::unordered_map<std::string, std::shared_ptr<Serializer>> kSerializers = {
   {"native", std::make_shared<NativeSerializer>()},
   {"xml", std::make_shared<XMLSerializer>()},
   {"json", std::make_shared<JsonSerializer>()},
   {"proto", std::make_shared<ProtoSerializer>()},
};

int main() {
    // GetResultController controller(&kSerializers);
    // ProxyServer server(std::stoi(std::getenv("PORT")), std::move(controller));
    // server.Start();
    SerializationTester tester;
    tester.Test(kSerializers.at("proto"), "proto");
    return 0;
}