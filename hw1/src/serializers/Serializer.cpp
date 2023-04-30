#include "Serializer.h"
#include <iostream>

TestData::TestData(int&& intValue, int64_t&& int64Value, double&& doubleField, std::string&& strValue, std::vector<int>&& vectorValue, std::map<std::string, int>&& mapValue)
: IntField(intValue), Int64Field(int64Value), DoubleField(doubleField), StrField(strValue), VectorField(vectorValue), MapField(mapValue) {}

int TestData::GetBytesSize() const {
    int mapSize = 0;
    for (const auto& [key, value] : MapField) {
        mapSize += sizeof(char) * key.size() + sizeof(int);
    }
    return sizeof(int) + sizeof(int64_t) + sizeof(double) + sizeof(char) * StrField.size() + sizeof(int) * VectorField.size() + mapSize;
}

std::ostream& operator<<(std::ostream& os, const TestData& testData) {
    os << testData.IntField << '\n';
    os << testData.Int64Field << '\n';
    os << testData.DoubleField << '\n';
    os << testData.StrField << '\n';
    for (const auto& el : testData.VectorField) {
        os << el << ' ';
    }
    os << '\n';
    for (const auto& [key, val] : testData.MapField) {
        os << key << ' ' << val << '\n';
    }
    return os;
}