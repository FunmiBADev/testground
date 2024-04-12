package org.kdb.inside.brains.credentials;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.kdb.inside.brains.core.credentials.CredentialsError;
import lombok.extern.slf4j.Slf4j;
import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.mockito.Mockito;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Objects;

import static org.junit.jupiter.api.Assertions.*;

public class SystemVarCredentialsEditorTest {
    private static final Logger log = LoggerFactory.getLogger(SystemVarCredentialsEditorTest.class);
    private SystemVarCredentialsEditor editor;

    @BeforeEach
    public void setUp() {
        editor = new SystemVarCredentialsEditor();
    }

    @Test
    public void testGetCredentials() {
        editor.setCredentials("username");
        String credentials = editor.getCredentials();
        assertEquals("username", credentials);
    }

    @Test
    public void testGetCredentialsJtp() {
        editor.setCredentials("testUser");
        assertEquals("testUser", editor.getCredentials());
    }

    @Test
    public void testGetViewableCredentials() {
        editor.setCredentials("username");
        String viewableCredentials = editor.getViewableCredentials();
        assertEquals("username", viewableCredentials);
    }

    @Test
    public void testSetCredentials() {
        editor.setCredentials("username");
        String credentials = editor.getCredentials();
        assertEquals("username", credentials);

        editor.setCredentials("new_username");
        credentials = editor.getCredentials();
        assertEquals("new_username", credentials);
    }

    @Test
    public void testSetCredentialsJtp() {
        editor.setCredentials("testUser");
        assertEquals("testUser", editor.getCredentials());
    }

    @Test
    public void testValidateEditorEmptyUsernameJtp() {
        editor.setCredentials("");
        System.out.println((editor));
        assertEquals(1, editor.validateEditor().size());
        System.out.println(String.valueOf(editor.validateEditor().size()));
        System.out.println((editor));
    }

    // Add more tests for validation with various scenarios

    // You may need to mock the necessary classes and methods for the next test

    // You may need to mock the necessary classes and methods for the next test
//    @Test
//    public void testAuthenticateWithCertificate() {
//        assertDoesNotThrow(() -> editor.authenticateWithCertificate());
//        // Ensure jwtToken is set after successful authentication
//        assertNotNull(editor.authenticateWithCertificate().);
//    }

//    @Test
//    public void testValidateEditorEmptyUsername() {
//        editor.setCredentials("");
//        List<CredentialsError> errors = editor.validateEditor();
//        assertEquals(1, errors.size());
//        assertEquals("Username can't be empty", errors.get(0).message());
//        assertEquals(editor.usernameField, errors.get(0).getComponent());
//    }
//
//    @Test
//    public void testValidateEditorSuccess() throws Exception {
//        editor.setCredentials("username");
//
//        SystemVarCredentialsProvider mockProvider = Mockito.mock(SystemVarCredentialsProvider.class);
//        Mockito.when(mockProvider.createEditor()).thenReturn(editor);
//        Mockito.when(editor.authenticateWithCertificate()).thenReturn("jwtToken");
//
//        List<CredentialsError> errors = editor.validateEditor();
//        assertEquals(0, errors.size());
//    }
//
//    @Test
//    public void testValidateEditorSuccess2() throws Exception {
//        editor.setCredentials("username");
//
//        SystemVarCredentialsProvider mockProvider = Mockito.mock(SystemVarCredentialsProvider.class);
//        Mockito.when(mockProvider.createEditor()).thenReturn(editor);
//
//        // Stubbing editor.authenticateWithCertificate() directly
//        Mockito.when(editor.authenticateWithCertificate()).thenReturn("jwtToken");
//
//        List<CredentialsError> errors = editor.validateEditor();
//        assertEquals(0, errors.size());
//    }


//    @Test
//    public void testValidateEditorAuthException() throws Exception {
//        editor.setCredentials("username");
//
//        Mockito.when(editor.authenticateWithCertificate()).thenThrow(new Exception("Authentication failed"));
//
//        List<CredentialsError> errors = editor.validateEditor();
//        assertEquals(1, errors.size());
//        assertTrue(errors.get(0).getMessage().contains("Error during certificate authentication"));
//        assertEquals(editor.usernameField, errors.get(0).getComponent());
//    }

//    @Test
//    public void testProcessCredentialChanged() {
//        CredentialEditor listener = Mockito.mock(CredentialEditor.class);
//        editor.addVetoableChangeListener(listener);
//
//        editor.usernameField.setText("username");
//
//        Mockito.verify(listener).credentialsChanged();
//    }


}
