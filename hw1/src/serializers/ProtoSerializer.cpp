#include "ProtoSerializer.h"
// #include "../lib/protos/test_data.pb.h"
#include <string>


std::string ProtoSerializer::Serialize(const TestData &testData) {
    // ProtoTestData protoTestData;
    // protoTestData.set_intfield(testData.IntField);
    // protoTestData.set_int64field(testData.Int64Field);
    // protoTestData.set_doublefield(testData.DoubleField);
    // protoTestData.set_strfield(testData.StrField);
    // for (int i = 0; i != testData.VectorField.size(); ++i) {
    //     protoTestData.set_vectorfield(i, testData.VectorField[i]);
    // }
    // auto it = testData.MapField.begin();
    // for (int i = 0; i != testData.MapField.size(); ++i) {
    //     MapFieldEntry* mapFieldEntry = protoTestData.add_mapfield();
    //     mapFieldEntry->set_key(it->first);
    //     mapFieldEntry->set_value(it->second);
    // }
    return "";//protoTestData.SerializeAsString();
}

TestData ProtoSerializer::Deserialize(const std::string& serializedData) {
    // ProtoTestData protoTestData;
    // protoTestData.ParseFromString(serializedData);
    // TestData testData;
    // testData.IntField = protoTestData.intfield();
    // testData.Int64Field = protoTestData.int64field();
    // testData.DoubleField = protoTestData.doublefield();
    // testData.StrField = protoTestData.strfield();
    // for (int i = 0; i != protoTestData.vectorfield().size(); ++i) {
    //     testData.VectorField.push_back(protoTestData.vectorfield().at(i));
    // }
    // for (int i = 0; i != protoTestData.mapfield().size(); ++i) {
    //     testData.MapField[protoTestData.mapfield().at(i).key()] = protoTestData.mapfield().at(i).value();
    // }
    // std::cout << serializedData << "\n\n\n";
    // std::cout << testData.IntField << ' ' << testData.Int64Field << ' ' << testData.DoubleField << ' ' << testData.StrField << '\n';
    // for (const auto& el : testData.VectorField) {
    //     std::cout << el << ' ';
    // }
    // std::cout << "\n\n";
    // for (const auto& [key, value] : testData.MapField) {
    //     std::cout << key << ' ' << value << '\n';
    // }
    // exit(0);
    // return testData;
    return {};
}