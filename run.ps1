./gradlew jar
Remove-Item -Recurse -Force build\libs\resources
Copy-Item -Recurse -Force src\main\resources build\libs\resources
java -jar build\libs\sfg-1.0-SNAPSHOT-all.jar
