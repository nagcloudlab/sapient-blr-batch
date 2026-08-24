# FoodExpress Order Service Dockerfile
# FIX: Changed from python:3.11 to eclipse-temurin:17-jre-alpine (Java 17 JRE)
FROM eclipse-temurin:17-jre-alpine

# FIX: Added WORKDIR for organized file layout
WORKDIR /app

# FIX: Corrected JAR filename to match actual build artifact
COPY target/order-service-1.0.0.jar app.jar

# Set environment variables
ENV SPRING_PROFILES_ACTIVE=production
ENV SERVER_PORT=8081

# FIX: Changed EXPOSE from 3000 to 8081 (Order Service port)
EXPOSE 8081

# FIX: Added non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# FIX: Corrected CMD to exec form with correct JAR path
CMD ["java", "-Xmx512m", "-jar", "app.jar"]

# FIX: Added HEALTHCHECK for orchestrator health monitoring
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8081/actuator/health || exit 1
