#pragma once

#include <vector>
#include <string>
#include <map>

struct TestData {
    int IntField;
    int64_t Int64Field;
    double DoubleField;
    std::string StrField;
    std::vector<int> VectorField;
    std::map<std::string, int> MapField;

    TestData() = default;

    TestData(int&& intValue, int64_t&& int64Value, double&& doubleField, std::string&& strValue, std::vector<int>&& vectorValue, std::map<std::string, int>&& mapValue);

    int GetBytesSize() const;
};

std::ostream& operator<<(std::ostream& os, const TestData& testData);

class Serializer {
public:
    virtual std::string Serialize(const TestData&) = 0;
    virtual TestData Deserialize(const std::string&) = 0;
    virtual ~Serializer() = default;
};