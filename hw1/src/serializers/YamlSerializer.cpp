#include "YamlSerializer.h"
#include <string>


std::string YamlSerializer::Serialize(const TestData &testData) {
    YAML::Node node;
    node["IntField"] = testData.IntField;
    node["Int64Field"] = testData.Int64Field;
    node["DoubleField"] = testData.DoubleField;
    node["StrField"] = testData.StrField;
    node["VectorField"] = testData.VectorField;
    node["MapField"] = testData.MapField;
    return YAML::Dump(node);
}
#include <iostream>
TestData YamlSerializer::Deserialize(const std::string& serializedData) {
    YAML::Node node = YAML::Load(serializedData);
    return {
        node["IntField"].as<int>(),
        node["Int64Field"].as<int64_t>(),
        node["DoubleField"].as<double>(),
        node["StrField"].as<std::string>(),
        node["VectorField"].as<std::vector<int>>(),
        node["MapField"].as<std::map<std::string, int>>(),
    };
}