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

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import javax.swing.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class UsernameCredentialsEditorRevampTest {

    private UsernameCredentialsEditorRevamp editor;

    @BeforeEach
    public void setUp() {
        editor = new UsernameCredentialsEditorRevamp();
    }

    @Test
    public void testProcessCredentialChanged_WithEmptyFields() {
        // Mocking the processCredentialChanged method
        UsernameCredentialsEditorRevamp spyEditor = spy(editor);

        editor.usernameField.setText("");
        editor.passwordField.setText("");

        spyEditor.processCredentialChanged(editor.getCredentials());

        // Assert that the method was called with empty credentials
        verify(spyEditor).processCredentialChanged("");
    }

    @Test
    public void testProcessCredentialChanged_WithNonEmptyFields() {
        // Mocking the processCredentialChanged method
        UsernameCredentialsEditorRevamp spyEditor = spy(editor);

        editor.usernameField.setText("username");
        editor.passwordField.setText("password");

        spyEditor.processCredentialChanged(editor.getCredentials());

        // Assert that the method was called with non-empty credentials
        verify(spyEditor).processCredentialChanged("username:password");
    }

    // You can write more tests to cover other scenarios or edge cases

}

