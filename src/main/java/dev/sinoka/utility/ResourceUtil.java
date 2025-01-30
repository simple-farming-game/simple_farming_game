package dev.sinoka.utility;

import java.io.File;
import java.net.URI;
import java.net.URL;
import java.nio.file.Path;
import java.nio.file.Paths;

public class ResourceUtil {

    public static String getAbsolutePath(String relativePath) {
        try {
            // JAR 파일 위치를 찾기 위해 현재 실행 중인 클래스의 URL을 얻음
            URL jarUrl = ResourceUtil.class.getProtectionDomain().getCodeSource().getLocation();
            File jarFile = new File(jarUrl.toURI());

            // JAR 파일이 있는 디렉토리 경로를 구함
            String jarDirectory = jarFile.getParent();

            // 상대 경로를 기준으로 절대 경로 계산
            Path absolutePath = Paths.get(jarDirectory, relativePath);
            return absolutePath.toString();
        } catch (Exception e) {
            throw new RuntimeException("Failed to resolve resource path: " + relativePath, e);
        }
    }
}
