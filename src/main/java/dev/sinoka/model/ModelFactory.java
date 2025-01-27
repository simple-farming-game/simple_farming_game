package dev.sinoka.model;

import dev.sinoka.utility.JsonFileReader;
import org.json.JSONArray;
import org.json.JSONObject;

public class ModelFactory {
    public static Model loadModelFromJson(String filePath) {
        // JSON 파일 읽기
        JsonFileReader jsonFileReader = new JsonFileReader(filePath);
        JSONObject jsonData = jsonFileReader.readJson();

        // 모델 정보 가져오기
        String modelName = jsonData.getString("name");
        JSONArray verticesArray = jsonData.getJSONArray("vertices");
        JSONArray indicesArray = jsonData.getJSONArray("indices");

        // Vertex 데이터 변환
        float[] vertices = new float[verticesArray.length()];
        for (int i = 0; i < verticesArray.length(); i++) {
            vertices[i] = verticesArray.getFloat(i);
        }

        // Index 데이터 변환
        int[] indices = new int[indicesArray.length()];
        for (int i = 0; i < indicesArray.length(); i++) {
            indices[i] = indicesArray.getInt(i);
        }

        // Model 객체 생성 및 반환
        return new Model(vertices, indices, modelName);
    }
}
