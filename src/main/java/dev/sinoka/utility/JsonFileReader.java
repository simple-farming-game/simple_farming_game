package dev.sinoka.utility;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class JsonFileReader {

    private static final Logger logger = LogManager.getLogger(JsonFileReader.class);

    private String filePath; // JSON 파일 경로

    /**
     * JsonFileReader 생성자
     * @param filePath 읽을 JSON 파일 경로
     */
    public JsonFileReader(String filePath) {
        this.filePath = filePath;
    }

    /**
     * JSON 파일 경로를 반환
     * @return 파일 경로
     */
    public String getFilePath() {
        return filePath;
    }

    /**
     * JSON 파일 경로를 설정
     * @param filePath 새로운 파일 경로
     */
    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    /**
     * 파일을 읽고 JSON 객체를 반환
     * @return JSON 객체 또는 null (오류 발생 시)
     */
    public JSONObject readJson() {
        try {
            // 파일 내용을 문자열로 읽기
            String content = new String(Files.readAllBytes(Paths.get(filePath)));

            // JSON 객체로 변환하여 반환
            return new JSONObject(content);
        } catch (IOException e) {
            System.err.println("JSON 파일 읽기 오류: " + e.getMessage());
            return null; // 오류 발생 시 null 반환
        }
    }

    /**
     * JSON 데이터를 출력
     */
    public void printJson() {
        JSONObject jsonObject = readJson();
        if (jsonObject != null) {
            logger.debug(jsonObject.toString(4)); // 들여쓰기 4칸으로 출력
        } else {
            logger.debug("JSON 데이터를 출력할 수 없습니다.");
        }
    }

    public static void main(String[] args) {
        // 테스트 예제
        String filePath = "path/to/your/file.json"; // JSON 파일 경로
        JsonFileReader reader = new JsonFileReader(filePath);

        // JSON 객체 출력
        reader.printJson();
    }
}
