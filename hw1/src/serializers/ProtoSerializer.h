#include "Serializer.h"

class ProtoSerializer : public Serializer {
public:
    std::string Serialize(const TestData& testData) override;
    TestData Deserialize(const std::string& serializedData) override;
};