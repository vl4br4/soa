#include "NativeSerializer.h"

DataForBinarySerialization::DataForBinarySerialization(TestData testData)
 : TestData(std::move(testData)) {}

void DataForBinarySerialization::save(std::ostringstream &oss) {
    boost::archive::binary_oarchive oa(oss);
    oa &*(this);
}

void DataForBinarySerialization::load(std::ostringstream &oss) {
    std::string str_data = oss.str();
    std::istringstream iss(str_data);
    boost::archive::binary_iarchive ia(iss);
    ia &*(this);
}

template <class Archive>
void DataForBinarySerialization::serialize(Archive& archive, const unsigned int version) {
    archive &IntField;
    archive &Int64Field;
    archive &DoubleField;
    archive &StrField;
    archive &VectorField;
    archive &MapField;
}

std::string NativeSerializer::Serialize(const TestData &testData) {
    DataForBinarySerialization data(testData);
    std::ostringstream oss;
    data.save(oss);
    return oss.str();
}

TestData NativeSerializer::Deserialize(const std::string& serializedData) {
    std::ostringstream oss(serializedData);
    DataForBinarySerialization data;
    data.load(oss);
    return data;
}