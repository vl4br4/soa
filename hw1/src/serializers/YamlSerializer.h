#include "Serializer.h"
#include "yaml-cpp/yaml.h"

class YamlSerializer : public Serializer {
public:
    std::string Serialize(const TestData& testData) override;
    TestData Deserialize(const std::string& serializedData) override;
};