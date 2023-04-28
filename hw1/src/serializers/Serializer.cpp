#include "Serializer.h"


TestData::TestData(int&& intValue, int64_t&& int64Value, double&& doubleField, std::string&& strValue, std::vector<int>&& vectorValue, std::map<std::string, int>&& mapValue)
: IntField(intValue), Int64Field(int64Value), DoubleField(doubleField), StrField(strValue), VectorField(vectorValue), MapField(mapValue) {}

int TestData::GetBytesSize() const {
    int mapSize = 0;
    for (const auto& [key, value] : MapField) {
        mapSize += sizeof(char) * key.size() + sizeof(int);
    }
    return sizeof(int) + sizeof(int64_t) + sizeof(double) + sizeof(char) * StrField.size() + sizeof(int) * VectorField.size() + mapSize;
}