import oasis.names.tc.xacml._3_0.core.schema.wd_17.AttributeDesignatorType;
import org.ow2.authzforce.core.pdp.api.*;
import org.ow2.authzforce.core.pdp.api.value.*;
import org.ow2.authzforce.xacml.identifiers.XacmlAttributeCategory;
import org.ow2.authzforce.xacml.identifiers.XacmlAttributeId;

import java.io.File;
import java.io.IOException;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Random;
import java.util.Set;

public class EnvironmentProvider extends BaseNamedAttributeProvider {

    private AttributeValueFactoryRegistry attributeValueFactoryRegistry;
    private AttributeProvider attributeProvider;

    public EnvironmentProvider(String instanceID) throws IllegalArgumentException {
        super(instanceID);
    }

    public EnvironmentProvider(AttributeValueFactoryRegistry attributeValueFactoryRegistry, AttributeProvider attributeProvider) throws IllegalArgumentException {
        super(String.valueOf(new Random().nextLong()));
        this.attributeProvider = attributeProvider;
        this.attributeValueFactoryRegistry = attributeValueFactoryRegistry;
    }


    @Override
    public void close() throws IOException {

    }


    @Override
    public Set<AttributeDesignatorType> getProvidedAttributes() {
        return Set.of(new AttributeDesignatorType(XacmlAttributeCategory.XACML_3_0_ENVIRONMENT.value(), XacmlAttributeId.XACML_1_0_ENVIRONMENT_CURRENT_TIME.value(), StandardDatatypes.TIME.toString(), null, false));
    }


    @Override
    public <AV extends AttributeValue> AttributeBag<AV> get(AttributeFqn attributeFqn, Datatype<AV> datatype, EvaluationContext evaluationContext) throws IndeterminateEvaluationException {

        if(attributeFqn.getCategory().equalsIgnoreCase(XacmlAttributeCategory.XACML_3_0_ENVIRONMENT.value())) {
            return new EnvironmentHandler<>(attributeFqn.getId(), datatype).retrieveAttribute();
        }
        return null;
    }
}