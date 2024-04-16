package org.kdb.inside.brains.credentials;

import lombok.extern.slf4j.Slf4j;
import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialProvider;
import org.kdb.inside.brains.core.credentials.CredentialsResolvingException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Slf4j
public class SystemVarCredentialsProvider implements CredentialProvider {
    public static final String SPLITTER = ":Bearer ";
    private static final Logger log = LoggerFactory.getLogger(SystemVarCredentialsProvider.class);

    @Override
    public String getName() {
        return "System Variable Credentials";
    }

    @Override
    public String getVersion() {
        return "2.0";
    }

    @Override
    public String getDescription() {
        return "Example of CredentialsPlugin that takes password from environment variables";
    }

    @Override
    public boolean isSupported(String credentials) {
        if (credentials == null) {
            return false;
        }
        return credentials.contains(SPLITTER);
    }

    public static String join(String u, String p) {
        return u + SPLITTER + p;
    }

    @Override
    public CredentialEditor createEditor() {
        return new SystemVarCredentialsEditor();
    }



    @Override
    public String resolveCredentials(String host, int port, String credentials) throws CredentialsResolvingException {
        final String[] v = split(credentials);
        if (v.length < 2) {
            throw new CredentialsResolvingException("Incorrect credentials format, no username provided ");
        }
        try {
            String jwtToken = new SystemVarCredentialsEditor().authenticateWithCertificate();
            return v[0] + ":" + jwtToken;
        } catch (Exception e) {
            log.error("Error Authenticating with certificate!", e);
            throw new CredentialsResolvingException("Error while resolving credentials: " + e.getMessage(), e);
        }
    }

    public static String[] split(String credentials) throws CredentialsResolvingException {
        int i = credentials.indexOf(SPLITTER);
        if (i < 0) {
            throw new CredentialsResolvingException("Incorrect credentials format, no :token: splitter");
        }
        return new String[]{credentials.substring(0, i), credentials.substring(i + SPLITTER.length())};
    }
}
