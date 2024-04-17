package org.kdb.inside.brains.credentials;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.kdb.inside.brains.core.credentials.CredentialEditor;

import static org.junit.jupiter.api.Assertions.*;

class UsernameCredentialsProviderRevampTest {
    private UsernameCredentialsProviderRevamp provider;
    @BeforeEach
    public void setUp() {
        provider = new UsernameCredentialsProviderRevamp();
    }

    @Test
    void testGetName() {
        String expectedName = "Fetch Token By Environment";
        String actualName = provider.getName();
        assertEquals(expectedName, actualName);

    }

    @Test
    void testGetVersion() {
        String expectedVersion = "For Intellij 2023";
        String actualVersion = provider.getVersion();
        assertEquals(expectedVersion, actualVersion);
    }

    @Test
    void testGetDescription() {

        String expectedDescription = "Compatible with Plugin 5.1";
        String actualDescription = provider.getDescription();
        assertEquals(expectedDescription, actualDescription);
    }

    @Test
    void testIsSupported_ValidCredentials() {
        String credentials = "username" + UsernameCredentialsProviderRevamp.SPLITTER + "token";
        boolean supported = provider.isSupported(credentials);
        assertTrue(supported);
    }

    @Test
    public void testIsNotSupported_InvalidCredentialsNoToken() {
        String credentials = "";
        boolean supported = provider.isSupported(credentials);
        assertFalse(supported);
    }

    @Test
    public void testCreateEditor() {
        UsernameCredentialsProviderRevamp provider = UsernameCredentialsProviderRevamp.INSTANCE;
        CredentialEditor editor = provider.createEditor();

        assertInstanceOf(UsernameCredentialsEditorRevamp.class, editor);
    }

    @Test
    public void testJoin() {
        String username = "test_user";
        String password = "Bearer eytokenpassword123";
        String expectedJoined = username + UsernameCredentialsProviderRevamp.SPLITTER + password;

        String joined = UsernameCredentialsProviderRevamp.join(username, password);

        assertEquals(expectedJoined, joined);
    }
}
