#include "Serializer.h"
#include <boost/archive/binary_iarchive.hpp>
#include <boost/archive/binary_oarchive.hpp>
#include <boost/serialization/vector.hpp>
#include <boost/serialization/map.hpp>
#include <sstream>

class DataForBinarySerialization : public TestData {
    friend class boost::serialization::access;
public:
    DataForBinarySerialization() = default;
    DataForBinarySerialization(TestData testData);

    template <class Archive>
    void serialize(Archive& archive, const unsigned int version);
    void save(std::ostringstream &oss);
    void load(std::ostringstream &oss);
};

class NativeSerializer : public Serializer {
public:
    std::string Serialize(const TestData& testData) override;
    TestData Deserialize(const std::string& serializedData) override;
};