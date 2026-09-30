package com.onlineshopping.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import java.util.List;

/**
 * Security settings loaded from application.yml under the 'app.security' prefix.
 * All features default to disabled when not configured.
 */
@Configuration
@ConfigurationProperties(prefix = "app.security")
public class WebSecurityProperties {

    private Csrf csrf = new Csrf();
    private Cors cors = new Cors();
    private Https https = new Https();

    public Csrf getCsrf() { return csrf; }
    public void setCsrf(Csrf csrf) { this.csrf = csrf; }

    public Cors getCors() { return cors; }
    public void setCors(Cors cors) { this.cors = cors; }

    public Https getHttps() { return https; }
    public void setHttps(Https https) { this.https = https; }

    public static class Csrf {
        private boolean enabled = false;
        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
    }

    public static class Cors {
        private boolean enabled = false;
        private List<String> allowedOrigins = List.of("*");
        private List<String> allowedMethods = List.of("GET", "POST", "PUT", "DELETE", "OPTIONS");
        private List<String> allowedHeaders = List.of("*");
        private boolean allowCredentials = false;
        private long maxAge = 3600L;

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
        public List<String> getAllowedOrigins() { return allowedOrigins; }
        public void setAllowedOrigins(List<String> allowedOrigins) { this.allowedOrigins = allowedOrigins; }
        public List<String> getAllowedMethods() { return allowedMethods; }
        public void setAllowedMethods(List<String> allowedMethods) { this.allowedMethods = allowedMethods; }
        public List<String> getAllowedHeaders() { return allowedHeaders; }
        public void setAllowedHeaders(List<String> allowedHeaders) { this.allowedHeaders = allowedHeaders; }
        public boolean isAllowCredentials() { return allowCredentials; }
        public void setAllowCredentials(boolean allowCredentials) { this.allowCredentials = allowCredentials; }
        public long getMaxAge() { return maxAge; }
        public void setMaxAge(long maxAge) { this.maxAge = maxAge; }
    }

    public static class Https {
        private boolean enabled = false;
        private boolean redirectHttp = false;
        private int httpsPort = 8443;

        public boolean isEnabled() { return enabled; }
        public void setEnabled(boolean enabled) { this.enabled = enabled; }
        public boolean isRedirectHttp() { return redirectHttp; }
        public void setRedirectHttp(boolean redirectHttp) { this.redirectHttp = redirectHttp; }
        public int getHttpsPort() { return httpsPort; }
        public void setHttpsPort(int httpsPort) { this.httpsPort = httpsPort; }
    }
}