# Frontend Dockerfile with multi-stage build pattern (node:18-alpine → nginx:alpine)
# Created with Docker AI (Gordon) best practices for security and efficiency
# Optimized for size < 200MB with security-first approach

# Build stage
FROM node:18-alpine AS builder

# Install minimal build dependencies in single layer with cleanup for smaller image
RUN apk add --no-cache python3 make g++ && \
    rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install production dependencies with security and efficiency optimizations
RUN npm ci --only=production --prefer-offline --no-audit --no-fund && \
    npm cache clean --force --silent && \
    rm -rf /root/.npm

# Copy source code
COPY . .

# Build the application with environment variable
ARG NEXT_PUBLIC_API_URL=http://localhost:8001
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

RUN npm run build

# Production stage
FROM nginx:alpine

# Install minimal runtime dependencies and clean cache in single layer
RUN apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

# Create dedicated non-root user for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copy nginx configuration with security hardening
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application from builder stage with proper ownership
COPY --from=builder --chown=appuser:appgroup /app/out /usr/share/nginx/html

# Copy environment setup script with proper permissions
COPY env.sh /env.sh
RUN chmod +x /env.sh && \
    chown appuser:appgroup /env.sh

# Set secure permissions on web content
RUN chown -R appuser:appgroup /usr/share/nginx/html && \
    chmod -R 644 /usr/share/nginx/html && \
    find /usr/share/nginx/html -type d -exec chmod 755 {} \;

# Create and set permissions for cache directories
RUN mkdir -p /var/cache/nginx/client_temp && \
    chown -R appuser:appgroup /var/cache/nginx && \
    chmod -R 755 /var/cache/nginx

# Expose port
EXPOSE 80

# Health check endpoint for container monitoring
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Start nginx as non-root user with environment variable support
USER appuser
CMD ["/env.sh"]