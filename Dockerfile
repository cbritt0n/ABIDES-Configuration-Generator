# ABIDES Configuration Generator v1.0.0 - Container Configuration
# Lightweight container for production-ready configuration generation

FROM python:3.11-slim

# Metadata
LABEL name="ABIDES Configuration Generator v1.0.0" \
      description="The definitive configuration generator for ABIDES market simulations" \
      version="1.0.0" \
      maintainer="ABIDES Development Team" \
      repository="https://github.com/jpmorganchase/abides-jpmc-public" \
      license="Apache-2.0"

# Environment setup for production
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Create application user for security
RUN groupadd --gid 1001 abides && \
    useradd --uid 1001 --gid abides --shell /bin/bash --create-home abides

# Create application directories
RUN mkdir -p /app/configs /app/output /app/logs && \
    chown -R abides:abides /app

# Set working directory
WORKDIR /app

# Copy the single-file application
COPY --chown=abides:abides configgen.py /app/
COPY --chown=abides:abides README.md /app/

# Copy requirements (though we have zero external dependencies)
COPY --chown=abides:abides requirements.txt /app/

# Make configgen.py executable
RUN chmod +x /app/configgen.py

# Switch to non-root user for security
USER abides

# Create volume mount points for output
VOLUME ["/app/configs", "/app/output", "/app/logs"]

# Health check - verify the application starts correctly
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python /app/configgen.py --help > /dev/null || exit 1

# Default entrypoint
ENTRYPOINT ["python", "/app/configgen.py"]

# Default command - show help
CMD ["--help"]

# Usage Examples:
# 
# Build:
#   docker build -t abides-configgen:v1.0.0 .
#
# List templates:
#   docker run --rm abides-configgen:v1.0.0 --list-templates
#
# Generate config with volume mount:
#   docker run --rm -v $(pwd)/output:/app/output \
#       abides-configgen:v2.0.0 \
#       --template rmsc03 -f docker_rmsc03 -o /app/output
#
# Interactive mode:
#   docker run --rm -it \
#       -v $(pwd)/configs:/app/configs \
#       abides-configgen:v2.0.0 bash
#
# Custom configuration:
#   docker run --rm -v $(pwd)/output:/app/output \
#       abides-configgen:v2.0.0 \
#       -f custom_sim -mm 5 -mo 10 -zi 100 --gym-mode -o /app/output