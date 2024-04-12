import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SystemVarCredentialsIntegrationTest {

    private SystemVarCredentialsProvider provider;
    private SystemVarCredentialsEditor editor;

    @BeforeEach
    public void setUp() {
        provider = new SystemVarCredentialsProvider();
        editor = new SystemVarCredentialsEditor();
        editor.setCredentials("testUser:token"); // Set some initial credentials
    }
@Test
public void testIntegratedSuccess() throws Exception {
  SystemVarCredentialsProvider provider = new SystemVarCredentialsProvider();
  SystemVarCredentialsEditor editor = provider.createEditor();
  editor.setCredentials("username");
  
  // Mock successful authentication (replace with actual logic)
  Mockito.when(editor.authenticateWithCertificate()).thenReturn("jwtToken");
  
  String credentials = provider.resolveCredentials("localhost", 8080, "username:token");
  assertEquals("username:jwtToken", credentials);
}

  @Test
public void testIntegratedValidationError() throws Exception {
  SystemVarCredentialsProvider provider = new SystemVarCredentialsProvider();
  SystemVarCredentialsEditor editor = provider.createEditor();
  editor.setCredentials("");
  
  try {
    provider.resolveCredentials("localhost", 8080, "");
    fail("Expected CredentialsResolvingException");
  } catch (CredentialsResolvingException e) {
    assertTrue(e.getMessage().contains("Username can't be empty"));
  }
}

  @Test
public void testIntegratedAuthError() throws Exception {
  SystemVarCredentialsProvider provider = new SystemVarCredentialsProvider();
  SystemVarCredentialsEditor editor = provider.createEditor();
  editor.setCredentials("username");
  
  // Mock authentication failure
  Mockito.when(editor.authenticateWithCertificate()).thenThrow(new Exception("Authentication failed"));
  
  try {
    provider.resolveCredentials("localhost", 8080, "username:token");
    fail("Expected CredentialsResolvingException");
  } catch (CredentialsResolvingException e) {
    assertTrue(e.getMessage().contains("Error while resolving credentials"));
  }
}

  @Test(expected = CredentialsResolvingException.class)
public void testIntegratedInvalidCredentialsFormat() throws Exception {
  SystemVarCredentialsProvider provider = new SystemVarCredentialsProvider();
  provider.resolveCredentials("localhost", 8080, "username");
}

    
}
