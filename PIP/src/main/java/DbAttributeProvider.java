import com.robertopoletti.dbprovider.AttributeProviderDescriptor;
import oasis.names.tc.xacml._3_0.core.schema.wd_17.Attribute;
import oasis.names.tc.xacml._3_0.core.schema.wd_17.AttributeDesignatorType;
import oasis.names.tc.xacml._3_0.core.schema.wd_17.Attributes;
import org.ow2.authzforce.core.pdp.api.*;
import org.ow2.authzforce.core.pdp.api.value.*;
import org.ow2.authzforce.xacml.identifiers.XacmlAttributeCategory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.sql.SQLException;
import java.util.*;

public class DbAttributeProvider extends BaseNamedAttributeProvider {
    private static final Logger logger = LoggerFactory.getLogger("com.robertopoletti");
    private AttributeValueFactoryRegistry attributeValueFactoryRegistry;
    private AttributeProvider attributeProvider;
    private AttributeProviderDescriptor descriptor;
    public DAO dao;

    public DbAttributeProvider(AttributeValueFactoryRegistry attributeValueFactoryRegistry, AttributeProvider attributeProvider, AttributeProviderDescriptor descriptor) throws IllegalArgumentException {
        super(String.valueOf(new Random().nextLong()));
        this.attributeProvider = attributeProvider;
        this.attributeValueFactoryRegistry = attributeValueFactoryRegistry;
        this.descriptor = descriptor;
        dao = new DAO();

    }

    @Override
    public void close() throws IOException {
        try {
            dao.closeConnection();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    //Called by PDP during its instantiation on the Attribute Provider. Let PDP know of which XACML attributes the Attribute Provider can provide.
    @Override
    public Set<AttributeDesignatorType> getProvidedAttributes() {
        List<AttributeDesignatorType> supportedAttributes = new ArrayList<>();
        for(Attributes attributes : descriptor.getAttributes()){
            for(Attribute attribute : attributes.getAttributes()) {
                supportedAttributes.add(new AttributeDesignatorType(attributes.getCategory(), attribute.getAttributeId(), attribute.getAttributeValues().get(0).getDataType(), null, false));
            }
        }
        logger.debug("DebugAtt:" + supportedAttributes.get(0).getAttributeId());
        return Set.copyOf(supportedAttributes);
    }

    //Called by PDP during policy evaluation in order to get missing attributes from this Attribute Provider.
    @Override
    public <AV extends AttributeValue> AttributeBag<AV> get(AttributeFqn attributeFqn, Datatype<AV> datatype, EvaluationContext evaluationContext) throws IndeterminateEvaluationException {

        if(attributeFqn.getCategory().equalsIgnoreCase(XacmlAttributeCategory.XACML_1_0_ACCESS_SUBJECT.value())) {
            return new AccessSubjectHandler<AV>(attributeFqn.getId(), datatype, evaluationContext, dao).retrieveAttribute();
        }
        return null;
    }
}