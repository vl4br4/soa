#include "XMLSerializer.h"
#include <iostream>

DataForXMLSerialization::DataForXMLSerialization(TestData testData)
 : TestData(std::move(testData)) {}

void DataForXMLSerialization::save(std::ostringstream &oss) {
    boost::archive::xml_oarchive oa(oss);
    oa << boost::serialization::make_nvp("TestData", *this);
}

void DataForXMLSerialization::load(std::ostringstream &oss) {
    
    std::string str_data = oss.str();
    std::istringstream iss(str_data);
    boost::archive::xml_iarchive ia(iss);
    ia >> boost::serialization::make_nvp("TestData", *this);
}

template <class Archive>
void DataForXMLSerialization::serialize(Archive& archive, const unsigned int version) {
    archive &boost::serialization::make_nvp("IntField", IntField);
    archive &boost::serialization::make_nvp("Int64Field", Int64Field);
    archive &boost::serialization::make_nvp("DoubleField", DoubleField);
    archive &boost::serialization::make_nvp("StrField", StrField);
    archive &boost::serialization::make_nvp("VectorField", VectorField);
    archive &boost::serialization::make_nvp("MapField", MapField);
}

std::string XMLSerializer::Serialize(const TestData &testData) {
    DataForXMLSerialization data(testData);
    std::ostringstream oss;
    data.save(oss);
    return oss.str();
}

TestData XMLSerializer::Deserialize(const std::string& serializedData) {
    std::ostringstream oss(serializedData);
    DataForXMLSerialization data;
    data.load(oss);
    return data;
}