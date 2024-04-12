import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SystemVarCredentialsProviderTest {
  private SystemVarCredentialsProvider provider;
  @BeforeEach
  public void setUp() {
        provider = new SystemVarCredentialsProvider();
    }
@Test
public void testGetName() {
  String expectedName = "System Variable Credentials";
  String actualName = provider.getName();
  assertEquals(expectedName, actualName);
}
@Test
public void testGetVersion() {
  String expectedVersion = "2.0";
  String actualVersion = provider.getVersion();
  assertEquals(expectedVersion, actualVersion);
}

@Test
public void testGetDescription() {
  String expectedDescription = "Example of CredentialsPlugin that takes password from environment variables";
  String actualDescription = provider.getDescription();
  assertEquals(expectedDescription, actualDescription);
}

@Test
public void testIsSupportedValidCredentials() {
  String credentials = "username" + SystemVarCredentialsProvider.SPLITTER + "token";
  boolean supported = provider.isSupported(credentials);
  assertTrue(supported);
}

@Test
public void testIsSupportedInvalidCredentialsNoToken() {
  String credentials = "username";
  boolean supported = provider.isSupported(credentials);
  assertFalse(supported);
}

@Test
public void testCreateEditor() {
  CredentialEditor editor = provider.createEditor();
  assertTrue(editor instanceof SystemVarCredentialsEditor);
}

@Test
public void testResolveCredentialsValid() throws Exception {
  String credentials = "username" + SystemVarCredentialsProvider.SPLITTER + "token";
  String host = "localhost";
  int port = 8080;
  
  SystemVarCredentialsProvider provider = new SystemVarCredentialsProvider();
  SystemVarCredentialsEditor mockEditor = Mockito.mock(SystemVarCredentialsEditor.class);
  Mockito.when(mockEditor.authenticateWithCertificate()).thenReturn("jwtToken");
  provider.setEditor(mockEditor);

  String resolvedCredentials = provider.resolveCredentials(host, port, credentials);
  String expectedCredentials = "username:jwtToken";
  assertEquals(expectedCredentials, resolvedCredentials);
}

@Test(expected = CredentialsResolvingException.class)
public void testResolveCredentialsInvalidNoUsername() throws Exception {
  String credentials = SystemVarCredentialsProvider.SPLITTER + "token";
  String host = "localhost";
  int port = 8080;
  
  provider.resolveCredentials(host, port, credentials);
}

//  Test resolveCredentials() method with exception in authenticateWithCertificate: (Mocking required)

// This test requires mocking the authenticateWithCertificate method of SystemVarCredentialsEditor class to throw an exception. Here's an example with Mockito:

@Test(expected = CredentialsResolvingException.class)
public void testResolveCredentialsException() throws Exception {
  String credentials = "username" + SystemVarCredentialsProvider.SPLITTER + "token";
  String host = "localhost";
  int port = 8080;
  
  SystemVarCredentialsEditor mockEditor = Mockito.mock(SystemVarCredentialsEditor.class);
  Mockito.when(mockEditor.authenticateWithCertificate()).thenThrow(new RuntimeException("Authentication failed"));
  provider.setEditor(mockEditor);

  provider.resolveCredentials(host, port, credentials);
}

@Test
public void testSplitValidCredentials() throws CredentialsResolvingException {
  String credentials = "username" + SystemVarCredentialsProvider.SPLITTER + "token";
  String[] expected = {"username", "token"};
  String[] actual = SystemVarCredentialsProvider.split(credentials);
  assertArrayEquals(expected, actual);
}
  
}


