#include "serializers/Serializer.h"
#include <memory>

class SerializationTester {
public:
    std::string Test(std::shared_ptr<Serializer> serialize, const std::string& method);
};