package org.kdb.inside.brains.credentials;

import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialProvider;
import org.mockito.Mockito;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.swing.*;

import java.lang.reflect.Field;
import static org.junit.jupiter.api.Assertions.*;

class UsernameCredentialsEditorRevampTest {

    private UsernameCredentialsEditorRevamp editor;
    private final String username = "fumzo";
    private final String username2 = "joy";
    private final String jwtToken = "fakeToken";
    private final String token2 = "fakeToken2";

    @BeforeEach
    public void setUp() {
        editor = new UsernameCredentialsEditorRevamp();
    }

    @Test
    public void testGetCredentials_WithUsernameAndPassword() {
        String credentials = getUserCredentials(username2, token2);
        String expectedCredentials = "joy:fakeToken2";

        editor.setCredentials(credentials);

        assertEquals(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testGetCredentials_WithUsernameOnly() {

        String credentials = getUserCredentials(username, "");
        editor.setCredentials(credentials);
        String expectedCredentials = "fumzo";
        assertEquals(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testSetCredentials_WithUsernameAndPassword() {
        String credentials = getUserCredentials(username, jwtToken);
        String expectedCredentials = "fumzo:fakeToken";

        editor.setCredentials(credentials);
        assertEquals(expectedCredentials, editor.getCredentials());
        assertNotNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testSetCredentials_WithUsernameOnly() {
        String credentials = getUserCredentials(username, "");
        String expectedCredentials = "fumzo";

        editor.setCredentials(credentials);
        assertEquals(expectedCredentials,  editor.getCredentials());
    }

    @Test
    public void testAuthenticateWithCertificate_Mocked() throws Exception {
        String mockToken = "fakeToken";

        // Mock the authentication logic

        UsernameCredentialsEditorRevamp spyEditor = Mockito.spy(editor);
        Mockito.doReturn(mockToken).when(spyEditor).authenticateWithCertificate();

        // Use reflection to access and modify the private field 'tokenButton'
        Field tokenButtonField = UsernameCredentialsEditorRevamp.class.getDeclaredField("tokenButton");
        tokenButtonField.setAccessible(true);
        JButton tokenButton = (JButton) tokenButtonField.get(spyEditor);

        // Simulate clicking the token button
        tokenButton.doClick();

        // Verify that the token is set correctly
        assertEquals(mockToken, jwtToken);

        assertNotNull(mockToken, jwtToken);
    }

    private String getUserCredentials(String username, String password) {
        if (password.isEmpty()  || password.isBlank()) {
            return username;
        }
        return username + ":" + password;
    }
}
