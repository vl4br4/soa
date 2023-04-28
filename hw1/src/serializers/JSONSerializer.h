#include "Serializer.h"
#include <nlohmann/json.hpp>

class JsonSerializer : public Serializer {
public:
    std::string Serialize(const TestData& testData) override;
    TestData Deserialize(const std::string& serializedData) override;
};