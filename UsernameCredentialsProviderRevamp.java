package org.kdb.inside.brains.credentials;

import lombok.extern.slf4j.Slf4j;
import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialProvider;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Slf4j
public class UsernameCredentialsProviderRevamp implements CredentialProvider {
    public static final String SPLITTER = ":";
    private static final Logger log = LoggerFactory.getLogger(UsernameCredentialsProviderRevamp.class);

    public static final UsernameCredentialsProviderRevamp INSTANCE = new UsernameCredentialsProviderRevamp();

    private UsernameCredentialsProviderRevamp() {
    }

    @Override
    public String getName() {
        return "Username/Password Credentials";
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
        return credentials != null;
    }

    @Override
    public CredentialEditor createEditor() {
        return new UsernameCredentialsEditorRevamp();
    }

    public static String join(String u, String p) {
        return u + SPLITTER + p;
    }
}
