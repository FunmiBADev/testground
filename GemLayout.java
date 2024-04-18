package org.kdb.inside.brains.credentials;

import lombok.extern.slf4j.Slf4j;
import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialsError;
import org.kdb.inside.brains.core.credentials.CredentialsResolvingException;

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Slf4j
public class UsernameCredentialsEditorRevamp extends CredentialEditor {
    private static final Logger log = LoggerFactory.getLogger(UsernameCredentialsEditorRevamp.class);
    private final JTextField usernameField = new JTextField();
    private final JComboBox<String> tokenDropdown = new JComboBox<>(new String[]{"Select From List", "Get UAT Token", "Get PROD Token"});
    private final JPasswordField passwordField = new JPasswordField();

    private String jwtToken = null;

    public UsernameCredentialsEditorRevamp() {

        final JPanel panel = new JPanel(new GridBagLayout());

        final GridBagConstraints cons = new GridBagConstraints();
        cons.insets = new Insets(3, 3, 3, 3);
        cons.fill = GridBagConstraints.HORIZONTAL;

        addField(panel, cons, "Username", usernameField);
        addField(panel, cons, "Password", passwordField);

        cons.gridx = 1;
        cons.weightx = 1;
        panel.add(tokenDropdown, cons);

        final DocumentListener documentListener = new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent documentEvent) {
                processCredentialChanged(getCredentials());
            }

            @Override
            public void removeUpdate(DocumentEvent documentEvent) {
                processCredentialChanged(getCredentials());
            }

            @Override
            public void changedUpdate(DocumentEvent documentEvent) {
                processCredentialChanged(getCredentials());
            }
        };

        usernameField.getDocument().addDocumentListener(documentListener);
        passwordField.getDocument().addDocumentListener(documentListener);

        tokenDropdown.addActionListener(e -> {
            try {

                String selectedOption = (String) tokenDropdown.getSelectedItem();
                String sessionToken = authenticateWithCertificate("www.uat.token.com");
                String uatSessionToken = authenticateWithCertificate("www.prod.token.com");

                if ("Get UAT Token".equals(selectedOption)) {
                    passwordField.setText(uatSessionToken);
                } else if ("Get PROD Token".equals(selectedOption)) {
                    passwordField.setText(sessionToken);
                } else {
                    throw new RuntimeException("Unknown token option selected");
                }

            } catch (Exception ex) {
                log.error("Error Authenticating with certificate!", ex);
                throw new RuntimeException(new CredentialsResolvingException("Error while resolving credentials: " + ex.getMessage(), ex));
            }
        });

        setLayout(new BorderLayout());
        add(panel, BorderLayout.NORTH);
    }

    private String authenticateWithCertificate(String tokenUrl) throws Exception {
        try {
            URL url = new URL(tokenUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            int responseCode = connection.getResponseCode();
            // Implement your token retrieval logic here
            jwtToken = readToken(connection);
            passwordField.setText(jwtToken);
            return jwtToken;
        } catch
