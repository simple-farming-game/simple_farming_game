call gradlew.bat jar
rd /s /q build\libs\resources
xcopy /e /i /h src\main\resources build\libs\resources
java -XstartOnFirstThread -jar build\libs\sfg-1.0-SNAPSHOT-all.jar
