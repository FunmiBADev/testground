import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SystemVarCredentialsEditorTest {
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
public void testValidateEditorEmptyUsername() {
  editor.setCredentials("");
  List<CredentialsError> errors = editor.validateEditor();
  assertEquals(1, errors.size());
  assertEquals("Username can't be empty", errors.get(0).getMessage());
  assertEquals(editor.usernameField, errors.get(0).getComponent());
}

@Test
public void testValidateEditorSuccess() throws Exception {
  editor.setCredentials("username");
  
  SystemVarCredentialsProvider mockProvider = Mockito.mock(SystemVarCredentialsProvider.class);
  Mockito.when(mockProvider.getEditor()).thenReturn(editor);
  Mockito.when(editor.authenticateWithCertificate()).thenReturn("jwtToken");
  
  List<CredentialsError> errors = editor.validateEditor();
  assertEquals(0, errors.size());
}

@Test
public void testValidateEditorAuthException() throws Exception {
  editor.setCredentials("username");
  
  Mockito.when(editor.authenticateWithCertificate()).thenThrow(new Exception("Authentication failed"));
  
  List<CredentialsError> errors = editor.validateEditor();
  assertEquals(1, errors.size());
  assertTrue(errors.get(0).getMessage().contains("Error during certificate authentication"));
  assertEquals(editor.usernameField, errors.get(0).getComponent());
}

@Test
public void testProcessCredentialChanged() {
  CredentialEditor.CredentialChangedListener listener = Mockito.mock(CredentialEditor.CredentialChangedListener.class);
  editor.addCredentialChangedListener(listener);
  
  editor.usernameField.setText("username");
  
  Mockito.verify(listener).credentialsChanged();
}


}




