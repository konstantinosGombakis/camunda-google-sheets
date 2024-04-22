FROM maven:3.8.3-openjdk-17 AS builder
COPY pom.xml .
COPY src ./src
RUN mvn clean install -Dmaven.test.skip=true

FROM openjdk:17
COPY --from=builder target/demo-app-1.0.0-SNAPSHOT.jar runner.jar
CMD ["java", "-jar", "runner.jar"]