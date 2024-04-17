package org.kdb.inside.brains.credentials;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.kdb.inside.brains.core.credentials.CredentialsError;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class UsernameCredentialsEditorRevampTest {

    private UsernameCredentialsEditorRevamp editor;
    private final String username = "fumzo";
    private final String username2 = "joy";
    private final String token = "fakeToken";
    private final String token2 = "fakeToken2";

    @BeforeEach
    public void setUp() {
        editor = new UsernameCredentialsEditorRevamp();
    }

    @Test
    public void testGetCredentials_EmptyPassword() {
        String credentials = getUserCredentials(username, "");
        String expectedCredentials = "fumzo";


        editor.setCredentials(credentials);
        assertEquals(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testGetCredentials_FilledUsernameAndPassword() {
        String credentials = getUserCredentials(username2, token2);
        String expectedCredentials = UsernameCredentialsProviderRevamp.join("joy", "fakeToken2");

        editor.setCredentials(credentials);
        assertEquals(expectedCredentials, editor.getCredentials());
        assertNotNull(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testGetViewableCredentials_EmptyPassword() {
        String credentials = getUserCredentials(username2, "");
        String expectedCredentials = "joy";

        editor.setCredentials(credentials);
        String viewableCredentials = editor.getViewableCredentials();

        assertEquals(expectedCredentials, viewableCredentials);
    }

    @Test
    public void testGetViewableCredentials_FilledUsernameAndPassword() {
        String credentials = getUserCredentials(username, token);
        String expectedCredentials = UsernameCredentialsProviderRevamp.join("fumzo", "*****");

        editor.setCredentials(credentials);
        String viewableCredentials = editor.getViewableCredentials();

        assertEquals(expectedCredentials, viewableCredentials);
        assertNotNull(expectedCredentials, viewableCredentials);
    }

    @Test
    public void testSetCredentials_NullCredentials() {
        String credentials = getUserCredentials("", "");
        String expectedCredentials = "";

        editor.setCredentials(credentials);

        assertEquals(expectedCredentials, editor.getCredentials());
    }

    @Test
    public void testValidateEditor_ValidUsernameAndPasswordCredentials() {
        String credentials = getUserCredentials(username, token);
        editor.setCredentials(credentials);

        List<CredentialsError> errors = editor.validateEditor();

        assertTrue(errors.isEmpty());
    }

    @Test
    public void testValidateEditor_EmptyUsernameError() {
        String credentials = getUserCredentials("", token2);
        editor.setCredentials(credentials);

        List<CredentialsError> errors = editor.validateEditor();

        assertFalse(errors.isEmpty());
        assertEquals(1, errors.size());
    }

    @Test
    public void testValidateEditor_EmptyPasswordError() {
        String credentials = getUserCredentials(username2, "");
        editor.setCredentials(credentials);

        List<CredentialsError> errors = editor.validateEditor();

        assertFalse(errors.isEmpty());
        assertEquals(1, errors.size());
    }

    @Test
    public void testValidateEditor_EmptyUsernamePasswordError() {
        String credentials = getUserCredentials("", "");
        editor.setCredentials(credentials);

        List<CredentialsError> errors = editor.validateEditor();

        assertFalse(errors.isEmpty());
        assertEquals(2, errors.size());
    }

    private String getUserCredentials(String username, String password) {
        if (password.isEmpty()  || password.isBlank()) {
            return username;
        }
        return username + ":" + password;
    }
}
