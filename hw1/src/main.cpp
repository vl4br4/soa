#include <string>
#include "proxy.h"
#include "serializers/NativeSerializer.h"
#include "serializers/XMLSerializer.h"
#include "serializers/JSONSerializer.h" 
#include "serializers/ProtoSerializer.h"
#include "serializers/YamlSerializer.h"
#include "serializers/AvroSerializer.h"
#include "serializers/MessagePackSerializer.h"
#include "SerializationTester.h"
#include <nlohmann/json.hpp>
#include "yaml-cpp/yaml.h"
#include "avro/Decoder.hh"


const static std::unordered_map<std::string, std::shared_ptr<Serializer>> kSerializers = {
   {"native", std::make_shared<NativeSerializer>()},
   {"xml", std::make_shared<XMLSerializer>()},
   {"json", std::make_shared<JsonSerializer>()},
   {"proto", std::make_shared<ProtoSerializer>()},
   {"avro", std::make_shared<AvroSerializer>()},
   {"mpack", std::make_shared<MessagePackSerializer>()},
};

int main() {
    GetResultController controller(&kSerializers);
    ProxyServer server(std::getenv("PORT") == nullptr ? 2000 : std::stoi(std::getenv("PO")), std::move(controller));
    server.Start();
    return 0;
}