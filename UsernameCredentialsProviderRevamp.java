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

    UsernameCredentialsProviderRevamp() {
    }

    @Override
    public String getName() {
        return "Fetch Token By Environment";
    }

    @Override
    public String getVersion() {
        return "For Intellij 2023";
    }

    @Override
    public String getDescription() {
        return "Compatible with Plugin 5.1";
    }

    @Override
    public boolean isSupported(String credentials) {
        if (credentials.isEmpty() || credentials.isBlank()) {
            return false;
        }
        return credentials.contains(SPLITTER);
    }

    @Override
    public CredentialEditor createEditor() {
        return new UsernameCredentialsEditorRevamp();
    }

    public static String join(String u, String p) {
        return u + SPLITTER + p;
    }
}
