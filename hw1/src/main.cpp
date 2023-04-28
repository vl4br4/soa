#include <string>
#include "proxy.h"
#include "serializers/NativeSerializer.h"

const static std::unordered_map<std::string, std::shared_ptr<Serializer>> kSerializers = {
  {"native", std::make_shared<NativeSerializer>()}
};

int main() {
  GetResultController controller(&kSerializers);
  ProxyServer server(std::stoi(std::getenv("PORT")), std::move(controller));
  server.Start();
  return 0;
}