#include "JSONSerializer.h"
#include <string>


std::string JsonSerializer::Serialize(const TestData &testData) {
    nlohmann::json j;
    j["IntField"] = testData.IntField;
    j["Int64Field"] = testData.Int64Field;
    j["DoubleField"] = testData.DoubleField;
    j["StrField"] = testData.StrField;
    j["VectorField"] = testData.VectorField;
    j["MapField"] = testData.MapField;
    return j.dump();
}

TestData JsonSerializer::Deserialize(const std::string& serializedData) {
    nlohmann::json j = nlohmann::json::parse(serializedData);
    return {
        j["IntField"].get<int>(),
        j["Int64Field"].get<int64_t>(),
        j["DoubleField"].get<double>(),
        j["StrField"].get<std::string>(),
        j["VectorField"].get<std::vector<int>>(),
        j["MapField"].get<std::map<std::string, int>>()
    };
}