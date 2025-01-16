package dev.sinoka.utility;

import java.net.URI;
import java.net.URL;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ResourceUtil {

    public static String getAbsolutePath(String relativePath) {
        try {
            // 리소스 URL 가져오기
            URL resourceURL = ResourceUtil.class.getClassLoader().getResource(relativePath);
            if (resourceURL == null) {
                throw new IllegalArgumentException("Resource not found: " + relativePath);
            }

            // URL을 URI로 변환 후 Path로 변환
            Path path = Paths.get(resourceURL.toURI());
            return path.toAbsolutePath().toString();

        } catch (Exception e) {
            throw new RuntimeException("Failed to resolve resource path: " + relativePath, e);
        }
    }
}
