package dev.sinoka.utility;

import org.joml.Matrix4f;
import org.joml.Vector3f;

public class MatUtil {

    public static Vector3f transformMatrixToVector(Matrix4f matrix, Vector3f vector) {
        // 벡터를 4D로 변환 (x, y, z, 1)
        Vector3f result = new Vector3f(vector);

        // 행렬과 벡터 곱셈 (4x4 * 4x1)
        Vector3f transformed = new Vector3f();
        matrix.transformPosition(result, transformed);

        // 새로운 벡터 반환
        return transformed;
    }
}
