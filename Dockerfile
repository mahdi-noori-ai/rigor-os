# syntax=docker/dockerfile:1.10
# Container image for shahrah-proxy.
#   docker build -t shahrah .
#   docker run -p 6432:6432 -e SHAHRAH_BACKEND=db:5432 ... shahrah
FROM rust:1-slim-trixie AS build
# pg_query needs libclang (bindgen) and protoc (prost-build).
RUN apt-get update && apt-get install -y --no-install-recommends \
        clang libclang-dev protobuf-compiler make \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY . .
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/src/target \
    cargo build --release --locked -p shahrah-proxy \
    && cp target/release/shahrah-proxy /usr/local/bin/shahrah-proxy

FROM debian:13-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin shahrah
COPY --from=build /usr/local/bin/shahrah-proxy /usr/local/bin/shahrah-proxy
USER shahrah
ENV SHAHRAH_LISTEN=0.0.0.0:6432 \
    RUST_LOG=info
EXPOSE 6432
ENTRYPOINT ["/usr/local/bin/shahrah-proxy"]
