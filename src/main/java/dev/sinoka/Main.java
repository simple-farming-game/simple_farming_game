package dev.sinoka;

import dev.sinoka.core.Application;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Main {
    public static void main(String[] args) {
        Application game = new Application();

        game.run();
    }
}
