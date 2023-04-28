#include "SerializationTester.h"
#include "tools/tick.h"

const static TestData kTestData(0xDEADBEEF, 99999999999999, 3.14, "hey ho", {8, 800, 555, 35, 35}, {{"worldWonder", 7}, {"damnDozen", 13}});

std::string SerializationTester::Test(std::shared_ptr<Serializer> serializer, const std::string& method) {
    int iterations = 1000;
    uint64_t meanSerializationTime = 0;
    uint64_t meanDeserializationTime = 0;

    for (int i = 0; i != iterations; ++i) {
        Tick serializationTick;
        std::string serialized = serializer->Serialize(kTestData);
        uint64_t serializationTime = serializationTick.Measure();

        Tick deserializationTick;
        TestData testData = serializer->Deserialize(serialized);
        uint64_t deserializationTime = serializationTick.Measure();

        meanSerializationTime += serializationTime / iterations;
        meanDeserializationTime += deserializationTime / iterations; 
    }

    return method + "-" + std::to_string(kTestData.GetBytesSize()) + "-" +
     std::to_string(meanSerializationTime) + "ms-" + std::to_string(meanDeserializationTime) + "ms";
}