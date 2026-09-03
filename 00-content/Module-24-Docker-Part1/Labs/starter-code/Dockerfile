# FoodExpress Order Service Dockerfile
# BUG: Wrong base image -- python:3.11 cannot run Java applications
FROM python:3.11-slim

# BUG: No WORKDIR set -- files will be copied to root directory
# Should have: WORKDIR /app

# BUG: Wrong JAR filename -- actual file is order-service-1.0.0.jar
COPY target/app.jar /application.jar

# Set environment variables
ENV SPRING_PROFILES_ACTIVE=production
ENV SERVER_PORT=8081

# BUG: Wrong port -- Order Service runs on 8081, not 3000
EXPOSE 3000

# BUG: No non-root user created
# Should have:
# RUN addgroup -S appgroup && adduser -S appuser -G appgroup
# USER appuser

# BUG: Wrong CMD syntax -- using shell form with incorrect path
# Should be exec form: CMD ["java", "-Xmx512m", "-jar", "app.jar"]
CMD java -jar /wrong-path/service.jar

# BUG: No HEALTHCHECK defined
# Should have:
# HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
#   CMD curl -f http://localhost:8081/actuator/health || exit 1
