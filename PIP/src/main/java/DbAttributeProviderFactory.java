import com.robertopoletti.dbprovider.AttributeProviderDescriptor;
import oasis.names.tc.xacml._3_0.core.schema.wd_17.AttributeDesignatorType;
import org.ow2.authzforce.core.pdp.api.AttributeProvider;
import org.ow2.authzforce.core.pdp.api.CloseableNamedAttributeProvider;
import org.ow2.authzforce.core.pdp.api.EnvironmentProperties;
import org.ow2.authzforce.core.pdp.api.value.AttributeValueFactoryRegistry;

import java.util.Set;

public class DbAttributeProviderFactory extends CloseableNamedAttributeProvider.FactoryBuilder<AttributeProviderDescriptor> {

    @Override
    public CloseableNamedAttributeProvider.DependencyAwareFactory getInstance(AttributeProviderDescriptor testAttributeProvider, EnvironmentProperties environmentProperties) throws IllegalArgumentException {
        return new CloseableNamedAttributeProvider.DependencyAwareFactory() {
            @Override
            public Set<AttributeDesignatorType> getDependencies() {
                return null;
            }

            //Create a new Subject Attribute Provider instance from a XML/JAXB configuration. It's called by PDP.
            @Override
            public CloseableNamedAttributeProvider getInstance(AttributeValueFactoryRegistry attributeValueFactoryRegistry, AttributeProvider attributeProvider) {
                return new DbAttributeProvider(attributeValueFactoryRegistry, attributeProvider, testAttributeProvider);
            }
        };
    }

    @Override
    public Class<AttributeProviderDescriptor> getJaxbClass() {
        return AttributeProviderDescriptor.class;
    }
}