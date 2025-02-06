./gradlew jar
rm -rf build/libs/resources
cp -r src/main/resources build/libs/resources
java -XstartOnFirstThread -jar build/libs/sfg-1.0-SNAPSHOT-all.jar