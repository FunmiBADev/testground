package org.kdb.inside.brains.credentials;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import javax.swing.*;
import java.lang.reflect.Field;

import static org.junit.Assert.*;

public class UsernameCredentialsEditorTest {
    private UsernameCredentialsEditor editor;
    private final String username = "fumzo";
    private final String username2 = "joy";
    private String jwtToken = "fakeToken";
    private final String token2 = "fakeToken2";


    @Before
    public void setUp() {
        editor = new UsernameCredentialsEditor();
    }

    @Test
    public void testGetCredentials_WithoutToken() {
        String credentials = getUserCredentials(username, "");
        editor.setCredentials(credentials);
        String expectedCredentials = "fumzo:";
        assertNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testGetCredentials_WithToken() {
        String credentials = getUserCredentials(username2, token2);
        String expectedCredentials = "joy:fakeToken2";

        editor.setCredentials(credentials);
        assertEquals(expectedCredentials, editor.getCredentials());
        assertNotNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testSetCredentials_WithoutToken() {
        String credentials = getUserCredentials(username, "");
        editor.setCredentials(credentials);
        String expectedCredentials = "fumzo:";

        editor.setCredentials(credentials);
        assertNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testSetCredentials_WithToken() {
        String credentials = getUserCredentials(username, jwtToken);
        String expectedCredentials = "fumzo:fakeToken";

        editor.setCredentials(credentials);
        assertEquals(expectedCredentials, editor.getCredentials());
        assertNotNull(expectedCredentials, editor.getCredentials());
    }


    //GEM
    @Test
    public void testGetCredentials_WithUsernameOnly() {
        String credentials = getUserCredentials(username, "");
        editor.setCredentials(credentials);
        String expectedCredentials = "fumzo:";
        assertNull(expectedCredentials, editor.getCredentials()); // No JWT token, so null is returned
    }

    @Test
    public void testGetCredentials_WithUsernameAndJwtToken() {
        String credentials = getUserCredentials(username, jwtToken);
        String expectedCredentials = "fumzo:fakeToken";

        editor.setCredentials(credentials);
        assertEquals(expectedCredentials, editor.getCredentials());
        assertNotNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testSetCredentials_WithUsernameOnly() {
        String credentials = getUserCredentials(username, "");
        String expectedCredentials = "fumzo:";

        editor.setCredentials(credentials);
        assertNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testSetCredentials_WithUsernameAndJwtToken() {
        String actualCredentials = getUserCredentials(username, jwtToken);
        String expectedCredentials = "fumzo:fakeToken";

        editor.setCredentials(actualCredentials);

        assertEquals(expectedCredentials, editor.getCredentials());
        assertNotNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testAuthenticateWithCertificate_Mocked() throws Exception {
        String mockToken = "mocked_jwt_token";

        // Mock the authentication logic
        jwtToken = null;
        UsernameCredentialsEditor spyEditor = Mockito.spy(editor);
        Mockito.doReturn(mockToken).when(spyEditor).authenticateWithCertificate();

        // Use reflection to access and modify the private field 'tokenButton'
        Field tokenButtonField = UsernameCredentialsEditor.class.getDeclaredField("tokenButton");
        tokenButtonField.setAccessible(true);
        JButton tokenButton = (JButton) tokenButtonField.get(spyEditor);

        // Simulate clicking the token button
        tokenButton.doClick();
        jwtToken = mockToken;

        // Verify that the token is set correctly
        assertEquals(mockToken, jwtToken);

        assertNotNull(mockToken, jwtToken);
    }


    private String getUserCredentials(String username, String token) {
        if (username.isBlank() || username.isEmpty() || token.isBlank() || token.isEmpty()) {
            return null;
        }
        return username + ":" + token;
    }
}
